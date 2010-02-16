//
//  InterfaceLayer.m
//  Genoma
//
//  Created by Giovanni Amati on 24/11/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "InterfaceLayer.h"
#import "SharedData.h"

#define SHIFT 10000 // shifta i tag degli item dei menu da 10000 in poi
#define MOVE 20

@implementation InterfaceLayer

-(id) init
{
	// always call "super" init
	// Apple recommends to re-assign "self" with the "super" return value
	if ((self = [super init]))
	{
		turn = NO;
		
		CCSprite *backmenu = [CCSprite spriteWithFile:@"back.png"];
		[backmenu setOpacity:100];
		[backmenu setPosition:ccp(4, 121)];
		[backmenu setAnchorPoint:ccp(0, 1)];
		[backmenu setVisible:NO];
		
		CCMenuItemImage *a1 = [CCMenuItemImage itemFromNormalImage:@"arrow2.png" selectedImage:@"arrow.png" target:self selector:@selector(upCallback:)];
		CCMenuItemImage *a2 = [CCMenuItemImage itemFromNormalImage:@"arrow2.png" selectedImage:@"arrow.png" target:self selector:@selector(downCallback:)];
		CCMenuItemImage *a3 = [CCMenuItemImage itemFromNormalImage:@"arrow2.png" selectedImage:@"arrow.png" target:self selector:@selector(leftCallback:)];
		CCMenuItemImage *a4 = [CCMenuItemImage itemFromNormalImage:@"arrow2.png" selectedImage:@"arrow.png" target:self selector:@selector(rightCallback:)];		
		
		[a1 setRotation:-90];
		[a2 setRotation:90];
		[a3 setRotation:-180];
		
		[a1 setPosition:ccp(407, 86)];
		[a2 setPosition:ccp(407, 28)];
		[a3 setPosition:ccp(364, 57)];
		[a4 setPosition:ccp(450, 57)];
		
		CCMenu *controller = [CCMenu menuWithItems:a1, a2, a3, a4, nil];
		[controller setOpacity:100];
		[controller setPosition:CGPointZero];
		[controller setVisible:NO];
		
		CGSize s = [[CCDirector sharedDirector] winSize];
		CCLabel *lturn = [CCLabel labelWithString:@"" dimensions:CGSizeMake(s.width, 44) alignment:UITextAlignmentCenter fontName:@"Lucon1" fontSize:18];
		[lturn setPosition:ccp(s.width/2, s.height/2+60)];
		id seq = [CCSequence actions:[CCFadeOut actionWithDuration:0.5], [CCFadeIn actionWithDuration:0.5], nil];
		[lturn runAction:[CCRepeatForever actionWithAction:seq]];
		
		[self addChild:backmenu z:0  tag:0];
		[self addChild:lturn z:0 tag:1];
		[self addChild:controller z:0 tag:2];
	}
	
	return self;
}

-(void) initMenu:(NSArray *)menuitems
{
	CCMenu *controller = (CCMenu *)[self getChildByTag:2];
	if (turn && ![controller visible])
	{
		CCSprite *backmenu = (CCSprite *)[self getChildByTag:0];
		[backmenu setVisible:YES];
		[controller setVisible:YES];
		
		int y = 56;
		for (NSString *item in menuitems)
		{
			CCLabel *lb = [CCLabel labelWithString:item dimensions:CGSizeMake(120, 28) alignment:UITextAlignmentLeft fontName:@"Lucon1" fontSize:14];
			lb.position = ccp(75, y);
			y -= MOVE;
			[self addChild:lb z:1 tag:num + SHIFT];
			[self configItem:num + SHIFT move:0];
			num += 1;
		}
	}
}

-(void) closeMenu
{
	CCMenu *controller = (CCMenu *)[self getChildByTag:2];
	if ([controller visible])
	{
		for (int i = 0 + SHIFT; i < num + SHIFT; i++) // clean
			[self removeChildByTag:i cleanup:TRUE];
		
		sel = 0;
		num = 0;
		
		CCSprite *backmenu = (CCSprite *)[self getChildByTag:0];
		[backmenu setVisible:NO];
		[controller setVisible:NO];
	}
}

-(void) configItem:(int)i move:(int)m
{
	CCLabel *lb = (CCLabel *)[self getChildByTag:i];
	[lb runAction:[CCMoveTo actionWithDuration:0.1 position:ccp(lb.position.x, lb.position.y + m)]];
	
	if (sel == i - SHIFT)
		[lb setOpacity:200];
	else if ((sel - 1 == i - SHIFT) || (sel + 1 == i - SHIFT))
		[lb setOpacity:100];
	else if ((sel - 2 == i - SHIFT) || (sel + 2 == i - SHIFT))
		[lb setOpacity:50];
	else
		[lb setOpacity:0];
}

-(void) setTurn:(NSString *)name
{
	CCLabel *lb = (CCLabel *)[self getChildByTag:1];
	if ([name isEqualToString:@"end"])
	{
		turn = NO;
		[self closeMenu];
		[lb setString:@"End of fight"];
	}
	else if ([name isEqualToString:@"you"])
	{
		turn = YES;
		[lb setString:@"It's your turn"];
	}
	else
	{
		turn = NO;
		[self closeMenu];
		[lb setString:[@"It's turn of " stringByAppendingString:name]];
	}
}

-(void) upCallback:(id)sender
{
	if (turn)
	{
		if (sel > 0)
		{
			sel -= 1;
			for (int i = 0 + SHIFT; i < num + SHIFT; i++)
				[self configItem:i move:-MOVE];
		}
	}
}

-(void) downCallback:(id)sender
{
	if (turn)
	{
		if (sel < num - 1) // occhio qua!!!!!!!!! - 1
		{
			sel += 1;
			for (int i = 0 + SHIFT; i < num + SHIFT; i++)
				[self configItem:i move:MOVE];
		}
	}
}

-(void) leftCallback:(id)sender
{
	if (turn)
	{
		CCLOG(@"Button left");
	}
}

-(void) rightCallback:(id)sender
{
	if (turn)
	{
		[[SharedData Initialize] menu:sel];
		[self closeMenu];
	}
}

// on "dealloc" you need to release all your retained objects
- (void) dealloc
{
	// in case you have something to dealloc, do it in this method
	// in this particular example nothing needs to be released.
	// cocos2d will automatically release all the children (Label)
	
	// don't forget to call "super dealloc"
	[super dealloc];
}

@end